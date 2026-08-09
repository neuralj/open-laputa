package app

import (
	"context"
	"log/slog"
)

func Run(ctx context.Context) error {
	slog.Info("service started")
	return nil
}
