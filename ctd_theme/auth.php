<?php
require dirname(__FILE__) . '/cos_sdk/vendor/autoload.php';

function get_auth_url($obj) {
    $secretId = "";
    $secretKey = "";
    $region = "";
    $cosClient = new Qcloud\Cos\Client(
        array(
            'region' => $region,
            'schema' => 'https',
            'credentials'=> array(
                'secretId'  => $secretId ,
                'secretKey' => $secretKey)));

    try {
        $bucket = "";
        $signedUrl = $cosClient->getObjectUrl($bucket, $obj, '+10 minutes');
        return $signedUrl;
    } catch (\Exception $e) {
        return -1;
    }
}