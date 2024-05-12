/* Import Libs */
import React, { useEffect, useState } from "react"
import styled from "styled-components"
import Loader from "react-spinners/BeatLoader"

/* Import Reusables Components */
import View from "../components/reusables/View"
import Modal from "../components/reusables/Modal"
import Table from "../components/Table"
import Button from "../components/Button"

import Exchange from "./Exchange"

/* Import WebApi */
import { list, remove, getBalance } from "../webapi/exchanges"
import { theme } from "../utils/theme"

const ExchangesStyle = styled.div`
  padding: 20px;
  width: 70%;

  & .loader {
    display: flex;
    justify-content: center;
  }

  & .actions {
    display: flex;
    justify-content: center;

    & .button-container {
      cursor: pointer;
      margin-right: 10px;
      color: white;
    }
  }
`

const Exchanges = () => {
  const [state, stateFunc] = useState({
    data: {},
  })

  const [addModal, addModalFunc] = useState({
    show: false,
  })

  const onToggleAddModal = () => {
    addModalFunc((prevState) => ({
      ...prevState,
      show: !prevState.show,
    }))
  }

  const onClickAdd = () => {
    addModalFunc((prevState) => ({
      ...prevState,
      show: true,
      id: "",
    }))
  }

  const onAdd = () => {
    getState()
  }

  const onEdit = (row) => {
    addModalFunc((prevState) => ({
      ...prevState,
      show: true,
      id: row.id,
    }))
  }

  const onDelete = (row) => {
    remove(row.id).then((_) => {
      getState()
    })
  }

  const transformToView = (data) => {
    return data
      .map((exchange) => ({
        ...exchange,
        balance: {
          loading: true,
          value: "",
        },
      }))
      .reduce((exchanges, exchange) => {
        return {
          ...exchanges,
          [exchange.id]: exchange,
        }
      }, {})
  }

  const getExchanges = () => {
    return new Promise((resolve, reject) => {
      list().then((response) => {
        stateFunc((prevState) => ({
          ...prevState,
          data: transformToView(response?.data || []),
        }))
        resolve(response.data)
      })
    })
  }

  const getState = () => {
    getExchanges().then((data) => {
      data.forEach((exchange) => {
        getBalance(exchange.id).then((response) => {
          stateFunc((prevState) => ({
            ...prevState,
            data: {
              ...prevState.data,
              [exchange.id]: {
                ...exchange,
                balance: {
                  loading: false,
                  value: response.data,
                },
              },
            },
          }))
        })
      })
    })
  }

  useEffect(() => {
    getState()
  }, []) // eslint-disable-line

  const headers = [
    {
      value: "alias",
      label: "Alias",
      default: true,
    },
    {
      value: "provider",
      label: "Provider",
    },
    {
      value: "balance",
      label: "Balance",
    },
    {
      value: "actions",
      label: "Actions",
    },
  ]

  const buildRow = (row) => {
    return [
      row.alias,
      "Binance",
      row.balance.loading ? (
        <div className="loader">
          <Loader size={8} color={theme.white} />
        </div>
      ) : (
        row.balance.value
      ),
      <div className="actions">
        <div className="button-container">
          <Button
            width={25}
            height={25}
            text={<i className="material-icons">edit</i>}
            tooltip="Edit"
            onClick={() => onEdit(row)}
            circle
          />
        </div>
        <div className="button-container">
          <Button
            width={25}
            height={25}
            text={<i className="material-icons">delete</i>}
            tooltip="Delete"
            onClick={() => onDelete(row)}
            circle
          />
        </div>
      </div>,
    ]
  }

  return (
    <>
      <Modal
        title="Exchange"
        content={
          <Exchange
            open={addModal.show}
            id={addModal.id}
            onCloseModal={onToggleAddModal}
            onAdd={onAdd}
          />
        }
        open={addModal.show}
        onToggleOpen={onToggleAddModal}
        width="900px"
      />
      <View
        title="Exchanges"
        buttons={[
          {
            icon: <i className="material-icons">add_circle</i>,
            label: "Add",
            onClick: onClickAdd,
          },
        ]}
        content={
          <ExchangesStyle>
            <Table
              headers={headers}
              data={Object.values(state.data)}
              buildRow={buildRow}
            />
          </ExchangesStyle>
        }
      />
    </>
  )
}

export default Exchanges
