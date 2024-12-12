package main

//请使用英文写commit message
type User struct {
	Account   string
	Password  string
	Isp       int
	UserAgent string
	v4ip      string //ipv4地址，成功登录后获得
}

var users []User

func addUser(account, password string, isp int, userAgent string) {
	new_user := User{
		Account:   account,
		Password:  password,
		Isp:       isp,
		UserAgent: userAgent,
		v4ip:      "",
	}
	users = append(users, new_user)
}
