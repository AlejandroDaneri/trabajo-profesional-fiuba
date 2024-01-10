package database

import "github.com/leesper/couchdb-golang"

type Strategy struct {
	PvtType string `json:"pvt_type"`
	StrategyPublicFields
	couchdb.Document
}

type Indicator struct {
	Name       string                 `json:"name"`
	Parameters map[string]interface{} `json:"parameters"`
}

const (
	StrategyStateRunning  = "running"
	StrategyStateFinished = "finished"
)

type StrategyPublicFields struct {
	State          string      `json:"state"`
	StartTimestamp int64       `json:"start_timestamp"`
	EndTimestamp   int64       `json:"end_timestamp"`
	Currencies     []string    `json:"currencies"`
	Indicators     []Indicator `json:"indicators"`
	Timeframe      string      `json:"timeframe"`
	InitialBalance int         `json:"initial_balance"`
	CurrentBalance string      `json:"current_balance"`
}
