<h1 align="center">AWS Service Health Dashboard Collector Plugin</h1>  

<br/>  
<div align="center" style="display:flex;">  
  <img width="245" src="https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-cloudservice.svg">
  <p> 
    <br>
    <img alt="Version"  src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000"  />    
    <a href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank"><img alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg" /></a> 
  </p> 
</div>   

##### Plugin to collect AWS Service Health Dashboard 

> SpaceONE's [plugin-aws-shd-inven-collector](https://github.com/spaceone-dev/plugin-aws-shd-inven-collector) is a convenient tool to get SHD(Service Heath Dashboard) from AWS.


Find us also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/aws-shd-inven-collector)
> Latest stable version : 1.0

Please contact us if you need any further information. (<support@spaceone.dev>)

---

## Collecting Contents

* Table of Contents
    * Event


---

## Authentication Overview

Registered service account on SpaceONE must have certain permissions to collect data Please, set
authentication privilege for followings:

<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "translate:TranslateText"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>


---
## Options

### Translate a description

If translate_enable is added to the list elements in options, Translate the description according to the value set in translate_options.
By default, `translate_enable` is `True` and `translate_options` example is below.

<pre>
<code>
{
    "translate_enable": true,
    "translate_options": {
        "source_lang_code": "en",
        "target_lang_code": "ko"
    } 
}
</code>
</pre>

The translated result is stored in `data.translate`.

<pre>
<code>

"data": {
    ....
    "translate": {
        "translate_enable": true,
        "translated_text": "EFS 및 FSx 원본 또는 대상 위치를 사용하여 DataSync 작업에 대해 오류 발생률이 높아지는 것을 계속 조사하여 “DataSync 대상 위치가 올바르게 마운트되지 않았습니다.”더 빨리 업데이트하지 않을 경우 오전 8시 (태평양 표준시 기준) 에 업데이트를 제공할 것입니다.",
        "translate_language": "ko"
    }
}
</code>
</pre>
