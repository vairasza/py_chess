# TL;DR:
# - Abgabe 2021-02-28
# - Header in main.py beachten

Modus der Prüfung
Als Abschlussarbeit ist eine Projektarbeit zu einem selbst gewählten Thema vorgesehen. Das Projekt kann alleine oder in Gruppen bis zu drei KursteilnehmerInnen bearbeitet werden. Unten ist eine Liste mit Themenvorschlägen, die in jedem Fall akzeptiert werden. Eigene Ideen bitte kurz mit mir durchsprechen, um den Aufwand zu klären.


Leitlinien für die Benotung
Ich werde mich bei der Notenvergabe an die folgenden Punkte halten:

- Grundanforderung für 4.0 ist, dass das Programm ausführbar ist, und den angekündigten Zweck erfüllt
- Sinnvolle Gliederung in Funktionen und Klassen gibt eine Notenstufe
- Sicherheitsfeatures (z.B. Abfangen von unsinnigen Eingaben, Prüfen ob notwendige Dateien existieren, ...) eine weitere
- Verwendung von vorgefertigten Methoden und Modulen (d.h. gute Kenntnis der eingebauten Methoden sowie von numpy et al) eine weitere.
  Abstufungen (also 1.7 statt 2.0) behalte ich mir für "Eleganz" vor. Redundanter Code kann also auch 0.3 Notenstufen kosten.


Schach-Interface
Eine sinnvolle Schach-KI zu entwickeln ist extrem aufwändig. Unter Interface ist hierbei lediglich ein Programm zu verstehen, das den Zustand eines Schachspiels im Speicher und auf dem Bildschirm abbildet, und den UserInnen die Möglichkeit gibt, Züge zu machen. Das Programm sollte abprüfen, ob der Zug erlaubt ist, und ob das Spiel bereits gewonnen ist.


Abgabe und Header
Auf GRIPS wird nach Kursende ein Upload geschalten, bei dem über den Zeitraum 2021-02-13 bis 2021-02-28 (etwas mehr als zwei Wochen) die Abgabe gemacht werden kann. Es ist möglich, bis Ende der Deadline Korrekturen vorzunehmen, d.h. eine erste Abgabe "zur Sicherheit" mit anschließender Verbesserung ist möglich. Pro Abgabegruppe reicht ein Upload. Der Upload soll den Python-Code sowie alle ggf. zur Ausführung nötigen Dateien enthalten (z.B. Textdateien, mit Fragen für ein Quiz, etc.). In den ersten Zeilen des Haupt-Code-Dokuments sollen Name und Matrikelnummer der Abgebenden als Kommentar vermerkt sein. Wenn Ihr Projekt aus mehreren Code-Dateien besteht, reicht diese Kommentare ins Hauptmodul zu schreiben. Bitte benennen Sie das Hauptmodul dann als main.py.

Der Kommentar kann so aussehen:
# ============================================================================ #
# Abgabe Projektarbeit Einführung ins Programmieren mit Python
# Namen
#     Magdalena Musterfrau, Mat.Nr. 123456
#     Max Mustermann, Mat.Nr. 654321