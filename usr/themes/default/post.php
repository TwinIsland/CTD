<?php if (!defined('__TYPECHO_ROOT_DIR__')) exit; ?>
<?php $this->need('header.php'); ?>

<div class="col-mb-12 col-8" id="main" role="main">
    <article class="post" itemscope itemtype="http://schema.org/BlogPosting">
        <h1 class="post-title" itemprop="name headline"><a itemprop="url" href="<?php $this->permalink() ?>"><?php $this->title() ?></a></h1>
        <ul class="post-meta">
            <li><?php _e('發布時間: '); ?><time datetime="<?php $this->date('c'); ?>" itemprop="datePublished"><?php $this->date(); ?></time></li>
        </ul>
        <div class="post-content" itemprop="articleBody">
            <?php
            $tag_total = explode(']',explode('[',$this->content)[1])[0];
            $tag = explode(',',$tag_total)[0];
            $content = $this->content;

            if($tag == 'book'){
                $url = explode(']',$content)[1];
                $url = str_replace(' ','%20',$url);
                $url = 'https://'.explode('.txt',explode('https://',$url)[1])[0].'.txt';
                $author = explode(',',$tag_total)[1];
                $age = explode(',',$tag_total)[2];
                $engine = 'https://www.baidu.com/s?wd=';
                if ($author == 'unknown' || $author == '佚名' && $age == 'unknown'){
                    $author = '未知';
                    $age = '未知';
                    echo '<br><strong>作者: </strong>'.$author;
                    echo '<br><strong>朝代: </strong>'.$age;
                }elseif ($author == 'unknown' || $author == '佚名'){
                    $author = '未知';
                    echo '<br><strong>作者: </strong>'.$author;
                    echo '<br><strong>朝代: </strong>'.'<a href="'.$engine.'朝代 '.$age.'" target=_blank>'.$age.'</a>';
                }elseif ($age == 'unknown'){
                    $age = '未知';
                    echo '<br><strong>作者: </strong>'.'<a href="'.$engine.'作者 '.$author.'" target=_blank>'.$author.'</a>';
                    echo '<br><strong>朝代: </strong>'.$age;
                }else{
                    echo '<br><strong>作者: </strong>'.'<a href="'.$engine.'作者 '.$author.'" target=_blank>'.$author.'</a>';
                    echo '<br><strong>朝代: </strong>'.'<a href="'.$engine.'朝代 '.$age.'" target=_blank>'.$age.'</a>';
                }

                echo '<hr>';
                $book_content =  file_get_contents($url);
                $trans_content = iconv("gbk", "utf-8//IGNORE",$book_content);
                if($trans_content == ''){
                    echo '<strong>不能成功加載資源</strong>';
                }else{
                    echo nl2br($trans_content);
                }
            }else{
                echo $content;
            }
            ?>
        </div>
        <div class="qr code">
            <?php
            echo '<center><img src="http://qr.topscan.com/api.php?text='.$this->permalink.'" alt="cannot load qr code" width=150</img></center>';
            ?>
        </div>
    </article>

    <?php $this->need('comments.php'); ?>

    <ul class="post-near">
        <li>上壹篇: <?php $this->thePrev('%s','沒有了'); ?></li>
        <li>下壹篇: <?php $this->theNext('%s','沒有了'); ?></li>
    </ul>
</div><!-- end #main-->

<?php $this->need('sidebar.php'); ?>
<?php $this->need('footer.php'); ?>


