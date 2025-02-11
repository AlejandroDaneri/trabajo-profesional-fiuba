package databaseservice

import (
	"fmt"
	"os"
	"sync"

	"github.com/leesper/couchdb-golang"
	"github.com/sirupsen/logrus"
)

var instance IService
var once sync.Once

func GetInstance() IService {
	once.Do(func() {
		instance = NewService()
	})
	return instance
}

type DatabaseService struct {
	couchdbClient *couchdb.Server
}

func NewService() IService {
	couchDBUser := os.Getenv("COUCHDB_USER")
	couchDBPassword := os.Getenv("COUCHDB_PASSWORD")
	couchDBHost := os.Getenv("COUCHDB_HOST")
	if couchDBHost == "" {
		couchDBHost = "couchdb"
	}
	client, err := couchdb.NewServer(fmt.Sprintf("http://%s:%s@%s:5984", couchDBUser, couchDBPassword, couchDBHost))
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Fatal("Could not connect to CouchDB")
	}
	return &DatabaseService{
		couchdbClient: client,
	}
}

type IService interface {
	GetDB(dbName string) (*couchdb.Database, error)
	CreateDB(dbName string) error
}

func (s *DatabaseService) GetDB(dbName string) (*couchdb.Database, error) {
	db, err := s.couchdbClient.Get(dbName)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":     err,
			"db name": dbName,
		}).Error("Could not get db")
		return nil, err
	}
	return db, nil
}

func (s *DatabaseService) CreateDB(dbName string) error {
	_, err := s.couchdbClient.Create(dbName)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":     err,
			"db name": dbName,
		}).Error("Could not create db")
		return err
	}
	return nil
}
