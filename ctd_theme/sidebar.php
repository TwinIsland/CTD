<?php if (!defined('__TYPECHO_ROOT_DIR__')) exit; ?>

<?php
$cos_url = "https://cdn.erdao.me/ctd"
?>

<div class="col-mb-12 col-offset-1 col-3 kit-hidden-tb" id="secondary" role="complementary">
    <?php if (!empty($this->options->sidebarBlock) && in_array('ShowRecentPosts', $this->options->sidebarBlock)): ?>

        <section class="widget">
            <h3 class="widget-title">收錄統計</h3>
            <?php Typecho_Widget::widget('Widget_Stat')->to($stat); ?>
            <p>本站藏書為: <?php echo  $stat->publishedPostsNum(); ?> 本</p>
        </section>
        <section class="widget">
            <h3 class="widget-title"><?php _e('最新發布'); ?></h3>
            <ul class="widget-list">
                <?php $this->widget('Widget_Contents_Post_Recent')
                    ->parse('<li><a href="{permalink}">{title}</a></li>'); ?>
            </ul>
        </section>
    <?php endif; ?>

    <section class="widget">
        <h3 class="widget-title"><?php _e('數據版本'); ?></h3>
        <p style="font-family: cursive"> <?php echo file_get_contents($cos_url.'/version') ?></p>
    </section>

</div><!-- end #sidebar -->
