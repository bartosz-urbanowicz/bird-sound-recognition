package models

import (
	"fmt"
	"net/http"
)

type Recording struct {
	RecordingID int    `json:"recording_id"`
	URL         string `json:"url"`
	UserID      string `json:"user_id"`
}

type RecordingList struct {
	Recordings []Recording `json:"recordings"`
}

func (recording *Recording) Bind(r *http.Request) error {
	if recording.URL == "" {
		return fmt.Errorf("url is a required field")
	}
	if recording.UserID == "" {
		return fmt.Errorf("user_id is a required field")
	}
	return nil
}
func (*RecordingList) Render(w http.ResponseWriter, r *http.Request) error {
	return nil
}
func (*Recording) Render(w http.ResponseWriter, r *http.Request) error {
	return nil
}
