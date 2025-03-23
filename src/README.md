## Receiver Device to the Fire Detection Egg for Firefighters

# Was war der Plan?

*Fire Detection Egg*:

Als Folge des Klimawandels wüten auf Korsika zunehmend mehr Waldbrände. Während die Telekommunikationsinfrastruktur in Städten mittlerweile eine meist lückenlose Abdeckung mit verfügbarer, schneller Datenübertragung aufweist, sind größere Waldflächen eine Herausforderung.
Einerseits ist es nicht wirtschaftlich, überall Masten aufzustellen und diese zu Warten, andererseits erhöhen diese sogar die Waldbrandgefahr (Quelle vom Miroboard einfg). Damit ist eine gute Echtzeitkommunikation über Distanz mit Wanderern oder Feuerwehrbodentruppen nur bedingt möglich. Worin sich auf direkt das nächste Problem zeigt: Eine Echtzeiterfassung darüber, welche Flächen brennen, ist derzeit kaum möglich. Satelliten betrachten nur wenige Male am Tag denselben Ort, sind darüber hinaus häufig optisch, sodass (Rauch-)Wolken die Sicht versperren, und selbst mit neueren Drohnenkonzepten dauert der Datenintegrationsprozess noch Stunden, nachdem das Gebiet überflogen wurde (Quelle).

Unser Konzept vom Fire Detection Egg soll daher am Boden eine Echtzeitübertragung über den Brandzustand liefern und über LoRa senden, falls ein Feuer detektiert wird. (Für weitere Details siehe Sender Device to the Fire Detection Egg)

In diesem Teil geht es darum, was mit den Daten gemacht wird, um im Einsatz nutzbar zu sein.

*Receiver Device*:

HW Idee: 
- GPS-Sensor
- LoRa Empfänger und Decoder
- Digitaler Kompass
- feuer- und wasserfestes, leichtes Design mit physischen Knöpfen zur intuitives und behandschuhten Benutzung 

Bekommt Egg ID zugesandt, ID korrespondiert mit Datenbankeintrag (gut dokumentierte GPS Locations der Egg IDs)

# Wie bin ich vorgegangen?

Nehmen wir mal an, die Hardware funktioniert: Wie würde unser User mit den Daten interagieren?

Eine Map, auf der der eigene Standort mit den Fire Detection Standorten in Verhältnis gesetzt wird, dargestellt auf einer Karte der Region mit den Höhenlinien (und später auch Flüssen)

Die Feuerorte werden mit einer Himmelsrichtung versehen.

# Wie könnte man weiterarbeiten?

HW basteln und Schnittstellen nutzen. 
Software Interrupts für die Aktualisierung
Effizientere Software (Beschleunigung der Funktionen durch Refactoring oder Wechsel/Fusion der Programmiersprache/-n)

