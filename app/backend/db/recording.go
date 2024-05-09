package db

import (
	"main/models"
)

func (db Database) getAllUserRecordings(userID int) (*models.RecordingList, error) {
	list := &models.RecordingList{}
	rows, err := db.Conn.Query(`SELECT * FROM recordings WHERE user_id == $1`, userID)
	if err != nil {
		return list, err
	}
	for rows.Next() {
		var recording models.Recording
		err := rows.Scan(&recording.RecordingID, &recording.URL, &recording.UserID)
		if err != nil {
			return list, err
		}
		list.Recordings = append(list.Recordings, recording)
	}
	return list, nil
}
func (db Database) addRecording(recording models.Recording) error {
	var recordingID int
	query := `INSERT INTO recordings (url, user_id) VALUES ($1, $2) RETURNING recording_id;`
	err := db.Conn.QueryRow(query, recording.URL, recording.UserID).Scan(&recordingID)
	if err != nil {
		return err
	}
	recording.RecordingID = recordingID
	return nil
}
