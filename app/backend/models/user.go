package models

import (
	"fmt"
	"net/http"
)

type User struct {
	UserID   int    `json:"user_id"`
	Username string `json:"username"`
}

func (u *User) Bind(r *http.Request) error {
	if u.Username == "" {
		return fmt.Errorf("username is a required field")
	}
	return nil
}

func (*User) Render(w http.ResponseWriter, r *http.Request) error {
	return nil
}
