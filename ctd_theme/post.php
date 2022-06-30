<?php if (!defined('__TYPECHO_ROOT_DIR__')) exit; ?>
<?php $this->need('header.php'); ?>
<?php require 'auth.php'?>


<?php
$base_url= $this->options->siteUrl;
?>

<?php
function get_encoding($test_str){
    if (mb_check_encoding($test_str, "gbk")){
        return "gbk";
    }
    if (mb_check_encoding($test_str, "utf-16")){
        return "utf-16";
    }
    if (mb_check_encoding($test_str, "UTF-16LE")){
        return "UTF-16LE";
    }
    if (mb_check_encoding($test_str, "cp1252")){
        return "cp1252";
    }
    return False;
}
?>
<div class="col-mb-12 col-8" id="main" role="main">
    <article class="post" itemscope itemtype="http://schema.org/BlogPosting">
        <h1 class="post-title" itemprop="name headline">
            <a itemprop="url"
               href="<?php $this->permalink() ?>"><?php $this->title() ?></a>
        </h1>
        <ul class="post-meta">
            <li><?php _e('作者: '); ?>
                <?php $author_data = str_replace('</p>',"", explode("|", $this->content)[1]); ?>
                <?php echo '<a href="'.$base_url.'/category/author_'.$author_data.'">'.$author_data.'</a>' ?>
            </li>
            <li><?php _e('朝代: '); ?>
            <?php $time_data = str_replace('<p>',"", explode("|", $this->content)[0]); ?>
                <?php echo '<a href="'.$base_url.'/category/period_'.$time_data.'">'.$time_data.'</a>' ?>
            </li>
            <?php 
            $cat = [];
            foreach ($this->categories as $item) {
                if (strpos($item["name"], 'period') === false and
                    strpos($item["name"], 'author') === false) {
                    array_push($cat, $item);
                }
            }
            ?>
            <?php 
            $cat_h = "";
            foreach ($cat as $item) {
                $cat_h = $cat_h.'<a href="'.$item["permalink"].'">'.$item["name"]."</a>, ";
            }
            ?>
            <li><?php _e('分类: '); ?><?php echo substr($cat_h,0, -2); ?></li>
        </ul>
        <br>
        <div class="post-content" itemprop="articleBody">
            <?php
            $content_url = get_auth_url('ctd/'.$this->cid.'.txt');
            if ($content_url == -1) {
                echo "sdk error";
            } else {
                $c = file_get_contents($content_url);
                $enc = get_encoding($c);
                if ($enc === False) {
                    echo "编码错误 cid_refer: " . $this->cid;
                } else {
                    echo nl2br(mb_convert_encoding($c, "utf-8", $enc));
                }
            }
            ?>
        </div>
    </article>

    <?php $this->need('comments.php'); ?>
</div><!-- end #main-->

<?php $this->need('sidebar.php'); ?>
<?php $this->need('footer.php'); ?>