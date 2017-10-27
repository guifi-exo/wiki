Requirements

Install `php-cs-fixer`, I will do it with docker

- Install docker
- Install [whalebrew](https://github.com/bfirsh/whalebrew)

Run the command

    sudo whalebrew install unibeautify/php-cs-fixer

or substitute its use (it does something like: creates a script that runs a docker and is available in $PATH)

Do everything inside the same directory

Put your .php file candidate. Let's use dnsservices.php

    wget https://raw.githubusercontent.com/guifi/dnsservices/master/dnsservices.php
    cp dnsservices.php dnsservices.php.bak

Create a file in the same directory with content `.php_cs`

```
echo <<EOF > .php_cs
<?php

return PhpCsFixer\Config::create()
    ->setUsingCache(false)
    ->setRules(array(
        '@PSR2' => true,
        '@Symfony' => true,
        'binary_operator_spaces' => true,
        'unary_operator_spaces' => true,
        'phpdoc_indent' => true,
        'whitespace_after_comma_in_array' => true,
        'concat_space' => array('spacing' => 'one'),
        'declare_equal_normalize' => array('space' => 'single'),
    ))
;
EOF
```

Execute

    php-cs-fixer fix dnsservices.php --diff

more rules/options here: https://github.com/FriendsOfPHP/PHP-CS-Fixer


Chunk example

``` diff
-    $hlastnow = @fopen($url."/guifi/refresh/dns", "r") or die('Error reading last dns refresh from remote server\n');
-    $last_now = fgets($hlastnow);
-    echo "Last server refreshed time: ".$last_now."\n";
-    fclose($hlastnow);
-    if (!file_exists("/tmp/last_update.dns")) {
-      $lastdns= @fopen("/tmp/last_update.dns", "w+") or die('Error!');
-      fwrite($lastdns,"0");
-      fclose($lastdns);
-   }
-    $hlast= @fopen("/tmp/last_update.dns", "r");
-    $last_local = fgets($hlast);
-    echo "Last local refreshed time: ".$last_local."\n";
-    if ($last_now === $last_local) {
-      fclose($hlast);
-      echo "No domain or/and hosts changes. Still fresh!\n";
-      return false;
-    }
-    else {
-      $hlast= @fopen("/tmp/last_update.dns", "w+") or die('Error!');
-      fwrite($hlast,$last_now);
-      fclose($hlast);
-      return true;
-    }
+      $hlastnow = @fopen($url . '/guifi/refresh/dns', 'r') or die('Error reading last dns refresh from remote server\n');
+      $last_now = fgets($hlastnow);
+      echo 'Last server refreshed time: ' . $last_now . "\n";
+      fclose($hlastnow);
+      if (!file_exists('/tmp/last_update.dns')) {
+          $lastdns = @fopen('/tmp/last_update.dns', 'w+') or die('Error!');
+          fwrite($lastdns, '0');
+          fclose($lastdns);
+      }
+      $hlast = @fopen('/tmp/last_update.dns', 'r');
+      $last_local = fgets($hlast);
+      echo 'Last local refreshed time: ' . $last_local . "\n";
+      if ($last_now === $last_local) {
+          fclose($hlast);
+          echo "No domain or/and hosts changes. Still fresh!\n";
+
+          return false;
+      } else {
+          $hlast = @fopen('/tmp/last_update.dns', 'w+') or die('Error!');
+          fwrite($hlast, $last_now);
+          fclose($hlast);
+
+          return true;
+      }
```
