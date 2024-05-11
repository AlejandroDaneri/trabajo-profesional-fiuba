/* Import Libs */
import React, { useEffect, useState } from "react"
import styled from "styled-components"
import Modal from "../components/reusables/Modal"

/* Import Reusables Components */
import View from "../components/reusables/View"
import Exchange from "./Exchange"
import { list, remove } from "../webapi/exchanges"
import Table from "../components/Table"
import Button from "../components/Button"

const ExchangesStyle = styled.div`
  padding: 20px;
  width: 70%;

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
    data: []
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

  const onAdd = () => {
  }

  const onDelete = (row) => {
    remove(row.id)
      .then(_ => {
        getState()
      })
  }

  const getState = () => {
    list()
      .then(response => {
        stateFunc(prevState => ({
          ...prevState,
          data: response?.data || []
        }))
      })
  }

  useEffect(() => {
    getState()
  }, [])

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
      value: "actions",
      label: "Actions",
    }
  ]

  const buildRow = (row) => {
    return [
      row.alias,
      'Binance',
      <div className="actions">
        <div className="button-container">
            <Button
              width={25}
              height={25}
              text={<i className="material-icons">edit</i>}
              tooltip="Edit"
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
      </div>
    ]
  }

  return (
    <>
      <Modal
        title="Exchange"
        content={<Exchange onCloseModal={onToggleAddModal} onAdd={onAdd} />}
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
            onClick: onToggleAddModal,
          },
        ]}
        content={
          <ExchangesStyle>
            <Table headers={headers} data={state.data} buildRow={buildRow} />
          </ExchangesStyle>
        }
      />
    </>
  );
};

export default Exchanges;
