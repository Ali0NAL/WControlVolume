El İzleme Tabanlı Ses Kontrolü

Bu Python programı, bir bilgisayarın ses seviyesini kontrol etmek için el izleme teknolojisini kullanır. Program, MediaPipe ve pycaw kütüphanelerini kullanarak işlevselliği sağlar.

Program, bir kamera (genellikle bir web kamerası ve ya bilgisayar kamerası) aracılığıyla el izleme yapar. MediaPipe kütüphanesi, el tespiti yapmak için kullanılır ve elde bulunan işaret ve başparmak arasındaki mesafeyi ölçer. Bu mesafe, ses seviyesini kontrol etmek için kullanılır.

İşaret ve başparmak arasındaki mesafe arttıkça, ses seviyesi artar; mesafe azaldıkça, ses seviyesi azalır. Bu, kullanıcının elini yukarı veya aşağı hareket ettirerek bilgisayarın ses seviyesini kontrol etmesine olanak tanır.

Ayrıca, program bir ilerleme çubuğu ile birlikte çalışır. Bu çubuk, el hareketine bağlı olarak ses seviyesini görsel olarak temsil eder. Ek olarak, ekranın sol üst köşesinde, işaretlenen ses seviyesini yüzde olarak gösteren bir metin bulunur.

Programın çalışması için bir web kamera gereklidir ve Python'un yanı sıra MediaPipe ve pycaw kütüphanelerinin yüklü olması gerekir.

Kullanım:

Programı çalıştırın.
Elinizi web kamerasına gösterin.
İşaret ve başparmak arasındaki mesafe değiştiğinde, ses seviyesi otomatik olarak ayarlanır.
Ses seviyesini kontrol etmek için elinizi yukarı veya aşağı hareket ettirin.
Programı kapatmak için klavyeden "q" tuşuna basın.
![volume](https://github.com/Ali0NAL/WControlVolume/assets/101065402/a56959b2-1d04-4241-b0c6-3f8642150993)
