<?php
    function allpostnum($id)
    {
        $db = Typecho_Db::get();
        $postnum = $db->fetchRow($db->select(array('COUNT(authorId)' => 'allpostnum'))->from('table.contents')->where('table.contents.authorId=?', $id)->where('table.contents.type=?', 'post'));
        $postnum = $postnum['allpostnum'];
        return $postnum;
    }

//µ÷ÓÃ echo allpostnum(1);