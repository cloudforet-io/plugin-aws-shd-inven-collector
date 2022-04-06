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

