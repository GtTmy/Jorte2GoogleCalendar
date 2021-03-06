# Jorte2GoogleCalendar
convert Jorte schedule data csv to google calendar via api 

please convert encoding of schedule_data.csv to utf-8 (w/o BOM)

## 概要
ジョルテからGoogleカレンダーに移行するために，データの移し替えを行うスクリプト．

ジョルテカレンダーのcsvを読み込んで，googleカレンダーに追加する．
ジョルテの吐く文字csvの文字コードはutf-8withBOMなので，あらかじめnkfなどでutf-8に変換しておく．

また，対象とするGoogleカレンダーアカウントでgoogle apiの認証をして，client_secret.jsonをおく．
[Googleのドキュメント](https://developers.google.com/google-apps/calendar/quickstart/python)を参考にした．
認証のコードもこのドキュメントを参考にしている．

挿入対象のGoogle Calendarはdefaultでは1つ目のカレンダー．カレンダーを指定するにはJorte2GoogleCalendar.pyでCALENDAR_IDを記述する．

スケジュール名，詳細，場所と時間のみ移行します．また，日本時間前提です．

## 参考
* [Google Calendar API Python quickstart](https://developers.google.com/google-apps/calendar/quickstart/python)
* [Google Calendar API Reference](https://developers.google.com/google-apps/calendar/v3/reference/)
* [PythonでGoogleカレンダーのAPIを叩く](http://taichino.com/programming/python-programming/3101)
