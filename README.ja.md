# server-metrics-2-ga

Google Analytics でサーバーの統計情報を記録するためのツールです。    
サーバーに、当ツールを配置 crontab で Google Analytics のプロパティ を指定して実行すると、指定したプロパティにサーバーの統計情報が Google Analytics のイベントとして記録されます。    

-------------------------------------------------------------
## Usage        

* git clone     
```console
git clone https://github.com/kemsakurai/server-metrics-2-ga.git    
```

* crontab example    
1分間隔で実行   
```console
*/1 * * * * /bin/python3.6 $SCRIPT_HOME/server-metrics-2-ga/server_metrics_2_ga.py -p UA-xxxxxxxx &>> $LOG_DIR/server_metrics_2_ga.log # server_metrics_2_ga.log
```   

* Image   
![2019-06-22 22.48.55.png - Google ドライブ](https://drive.google.com/uc?export=view&id=16bts0e1qVcPxc0e6An7Pz84BP1Zs6Eqw)

------------------------------------------------------------
## Scripts    

* `server-metrics-2-ga.py`    
取得するメトリクスを1指標ごとにGAイベントとして送信するスクリプトです。    

* `server-metrics-2-ga_with_cd.py`    
取得するメトリクスを複数指標ごとにGAイベントとして送信するスクリプトです。        
複数送信される指標はカスタムディメンションに設定します。     

--------------------------------------
## Blog     
* [サーバー指標 を Google Analytics に記録する | Monotalk](https://www.monotalk.xyz/blog/Record-server-metrics-in-Google-Analytics/)   
