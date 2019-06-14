<?php

function read_rss($rss_r)
{
    $xml = simplexml_load_file($rss_r);
    foreach ($xml->channel->item as $item) {
        $decode_c = base64_encode($rss_r.'-'.$item->link);
        $link = '/api/wechat.php?read='.$decode_c;
        echo '<a href="' . $link . '" target="_blank">';
        echo $item->title;
        echo '</a>';
        echo '<br><br>';
        //$des = str_replace(' ', '', str_replace('	', '', strip_tags($item->description)));
        //$des = str_replace("\n", '', $des);
        //$des = str_replace("\r", '', $des);
        //$des = explode(' ',$des)[0];
        //echo $des;
        //echo '<br/><br>';
    }
}

if (isset($_GET['id'])) {
    echo '<h1>OverFit API</h1>';
    echo '<h3>click to read</h3>';
    echo '<hr>';
    read_rss('https://rsshub.app/wechat/csm/'.$_GET['id']);
}elseif(isset($_GET['read'])){
    echo '<h1>OverFit API</h1>';
    echo '<h3>Reading Page</h3>';
    echo '<hr>';
    $c = base64_decode($_GET['read']);
    $rss_r = explode('-',$c)[0];
    $rss_link = explode('-',$c)[1];
    $xml = simplexml_load_file($rss_r);
    foreach ($xml->channel->item as $item) {
        if($item->link == $rss_link){
            $des = str_replace(' ', '', str_replace('	', '', strip_tags($item->description)));
            $des = str_replace("\n", '', $des);
            $des = str_replace("\r", '', $des);
            echo $des;
            break;
        }
    }
}
else{
    echo '<h1>OverFit API</h1><p>Sorry, but there is a bug...</p>';
}



