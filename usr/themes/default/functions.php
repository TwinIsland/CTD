<?php
if (!defined('__TYPECHO_ROOT_DIR__')) exit;

function themeConfig($form) {
    $logoUrl = new Typecho_Widget_Helper_Form_Element_Text('logoUrl', NULL, NULL, _t('站點 LOGO 地址'), _t('在這裏填入壹個圖片 URL 地址, 以在網站標題前加上壹個 LOGO'));
    $form->addInput($logoUrl);
    
    $sidebarBlock = new Typecho_Widget_Helper_Form_Element_Checkbox('sidebarBlock', 
    array('ShowRecentPosts' => _t('顯示最新文章'),
    'ShowRecentComments' => _t('顯示最近回復'),
    'ShowCategory' => _t('顯示分類'),
    'ShowArchive' => _t('顯示歸檔'),
    'ShowOther' => _t('顯示其它雜項')),
    array('ShowRecentPosts', 'ShowRecentComments', 'ShowCategory', 'ShowArchive', 'ShowOther'), _t('側邊欄顯示'));
    
    $form->addInput($sidebarBlock->multiMode());
}


/*
function themeFields($layout) {
    $logoUrl = new Typecho_Widget_Helper_Form_Element_Text('logoUrl', NULL, NULL, _t('站點LOGO地址'), _t('在這裏填入壹個圖片URL地址, 以在網站標題前加上壹個LOGO'));
    $layout->addItem($logoUrl);
}
*/

function allpostnum($id){
$db = Typecho_Db::get();
$postnum=$db->fetchRow($db->select(array('COUNT(authorId)'=>'allpostnum'))->from ('table.contents')->where ('table.contents.authorId=?',$id)->where('table.contents.type=?', 'post'));
$postnum = $postnum['allpostnum'];
return $postnum;
}
