# weibo-backup-toolkit

## Dumper
### Run
```
> python dump.py [-n N] uid
```

## TODO
* A processor that 
  * converts "created_at" to correct timestamp.
  * merges raw pages from relative view to absolute view.
  * download images.
* Some kind of presentation.

## Finding UID
Go to https://m.weibo.cn and go to your own page.

In the URL find the numbers and that's your UID.

> https://m.weibo.cn/u/1691705075 -> UID: 1691705075
