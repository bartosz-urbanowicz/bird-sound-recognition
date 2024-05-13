package handler

import (
	"context"
	"fmt"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/render"
	"main/db"
	"net/http"
	"strconv"
)

func recordings(router chi.Router) {
	router.Route("/{userID}", func(router chi.Router) {
		router.Use(UserContext)
		router.Get("/", getUserRecordings)
	})
}

func UserContext(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		userID := chi.URLParam(r, "userID")
		if userID == "" {
			render.Render(w, r, ErrorRenderer(fmt.Errorf("user ID is required")))
			return
		}
		id, err := strconv.Atoi(userID)
		if err != nil {
			render.Render(w, r, ErrorRenderer(fmt.Errorf("invalid user ID")))
		}
		ctx := context.WithValue(r.Context(), "userID", id)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

func getUserRecordings(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("userID").(int)
	recordings, err := dbInstance.GetAllUserRecordings(userID)
	if err != nil {
		if err == db.ErrNoMatch {
			render.Render(w, r, ErrNotFound)
		} else {
			render.Render(w, r, ErrorRenderer(err))
		}
		return
	}
	if err := render.Render(w, r, recordings); err != nil {
		render.Render(w, r, ServerErrorRenderer(err))
		return
	}
}
