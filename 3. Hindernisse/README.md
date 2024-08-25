**Programmierung Hindernisrennen**

Beim Hindernisrennen nutzen wir die Programmierung vom Eröffnungsrennen als Grundlage, da wir auch hier autonom fahren müssen. Nur wenn die Kamera einen bunten Stein erkennt, sendet der obere Raspberrypi ein Signal an den fahrenden Raspberrypi dieser führt dann ein demenstsprechendes Ausweichmannöver aus. Bei roten Steinen fahren wir rechts herum, bei grünen Steinen links herum. Desweiteren erkennen wir über den Farbsensor Kurven, dort führen wir dann nämlich ein Ausrichtungsmannöver aus. Für die Farberkennung der Klötze verwenden wir Filter/Masken, um nur die Farben zu sehen und andere Fehler, die die Kamera erkennen könnte, auszublenden. Dort erkennen wir dann Kontouren. Zum Einstellen der Farbwerte der Masken haben wir uns ein extra script mit Schiebereglern geschrieben.

**Darstellung der Erkennung:**


![IMG_9805 2](https://github.com/NickTechMaster/WRO_Future_Engineers_MKS_Robotics_2023/assets/80636354/3a39df79-cf18-4d0a-bdf5-776c626a113e)
