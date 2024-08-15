FROM php:latest

# Gerekli PHP modül ve paketlerini yükleme (opsiyonel, ihtiyacınıza göre değiştirin)
RUN docker-php-ext-install pdo_mysql mysqli

# Uygulama dosyalarını kopyalama
WORKDIR /var/www/html
COPY . .

# PHP içinde çalışacak HTTP sunucusunu başlatma
CMD ["php", "-S", "0.0.0.0:8080", "xss_scanner.php"]
