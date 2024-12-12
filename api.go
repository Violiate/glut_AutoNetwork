package main

import (
	"fmt"
	"io"
	"net/http"
	"regexp"
)

type User struct {
	Account   string
	Password  string
	Isp       int
	UserAgent string
	v4ip      string //ipv4地址，成功登录后获得
}

var UserAgentList = []string{
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
	"Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/131.0.0.0",
}

func login(user User) {
	url := fmt.Sprintf("http://172.16.2.2/drcom/login?callback=dr1003&DDDDD=%s&upass=%s&0MKKey=123456&R1=0&R2=&R3=3&R6=0&para=00&v6ip=&terminal_type=1&lang=zh-cn&jsVersion=4.1&v=2230&lang=zh", user.Account, user.Password)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println("http.NewRequest err:", err)
		return
	}
	req.Header.Set("Accept", "*/*")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6")
	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("Referer", "http://172.16.2.2/")
	req.Header.Set("User-Agent", user.UserAgent)
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error making request:", err)
		return
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading body:", err)
		return
	}
	fmt.Println(string(body))
}

func check_connect(user User) bool {
	url := "http://172.16.2.2/"
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println("http.NewRequest err:", err)
		return false
	}
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6")
	req.Header.Set("Cache-Control", "max-age=0")
	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("Upgrade-Insecure-Requests", "1")
	req.Header.Set("User-Agent", user.UserAgent)
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error making request:", err)
		return false
	}
	defer resp.Body.Close()
	text, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading body:", err)
		return false
	}
	htmltext := string(text)
	//正则获得ip和账号
	//uidRegex := regexp.MustCompile(`uid='([^']+)'`)
	//uid:=uidRegex.FindStringSubmatch(htmltext)
	v4ipRegex := regexp.MustCompile(`v4ip='([^']+)'`)
	v4ip := v4ipRegex.FindStringSubmatch(htmltext)
	if len(v4ip) > 1 {
		user.v4ip = v4ip[1]
		fmt.Println("v4ip:", user.v4ip)
		return true
	} else {
		fmt.Println("v4ip not found")
		return false
	}

}
