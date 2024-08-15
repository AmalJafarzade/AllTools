<?php

// URL'yi POST isteğinden al
$url = $_POST['url'];

// XSS vektörlerini tanımla
$xss_vectors = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>"
    // Diğer XSS vektörleri buraya eklenebilir
];

// Her bir XSS vektörü için test yap
foreach ($xss_vectors as $vector) {
    // XSS vektörünü URL'ye ekleyerek tam URL oluştur
    $test_url = $url . urlencode($vector);

    // URL'yi ziyaret et ve içeriği al
    $response = @file_get_contents($test_url);

    // Cevapta XSS vektörü var mı kontrol et
    if ($response !== false && strpos($response, $vector) !== false) {
        echo "XSS açığı bulundu: $vector\n";
    } else {
        echo "XSS açığı bulunamadı: $vector\n";
    }
}
?>
