<?php if (!defined('__TYPECHO_ROOT_DIR__')) exit; ?>
<div class="col-mb-12 col-offset-1 col-3 kit-hidden-tb" id="secondary" role="complementary">
    <?php if (!empty($this->options->sidebarBlock) && in_array('ShowRecentPosts', $this->options->sidebarBlock)): ?>

        <section class="widget">
            <h3 class="widget-title">收錄統計</h3>
            <p>本站藏書為: <?php echo allpostnum(1); ?> 本</p>
            <blockquote>已於2019年6月6日處理加新增書籍786本</blockquote>
        </section>
        <section class="widget">
            <h3 class="widget-title"><?php _e('最新發布'); ?></h3>
            <ul class="widget-list">
                <?php $this->widget('Widget_Contents_Post_Recent')
                    ->parse('<li><a href="{permalink}">{title}</a></li>'); ?>
            </ul>
        </section>
    <?php endif; ?>

    <?php if (!empty($this->options->sidebarBlock) && in_array('ShowRecentComments', $this->options->sidebarBlock)): ?>
        <section class="widget">
            <h3 class="widget-title"><?php _e('最近書評'); ?></h3>
            <ul class="widget-list">
                <?php $this->widget('Widget_Comments_Recent')->to($comments); ?>
                <?php while($comments->next()): ?>
                    <li><a href="<?php $comments->permalink(); ?>"><?php $comments->author(false); ?></a>: <?php $comments->excerpt(35, '...'); ?></li>
                <?php endwhile; ?>
            </ul>
        </section>
    <?php endif; ?>


</div><!-- end #sidebar -->
