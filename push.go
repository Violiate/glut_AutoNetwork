package main

import (
	"fmt"
	"os/exec"
)

func push(message string) error {
	cmd := exec.Command("python3", "push.py", message)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("推送失败")
		fmt.Println(err)
		return err
	}
	fmt.Println("推送成功")
	fmt.Println(string(output))
	return nil

}
