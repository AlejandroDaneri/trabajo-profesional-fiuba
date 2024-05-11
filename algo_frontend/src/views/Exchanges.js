/* Import Libs */
import React, { useEffect, useState } from "react"
import styled from "styled-components"
import Modal from "../components/reusables/Modal"

/* Import Reusables Components */
import View from "../components/reusables/View"
import Exchange from "./Exchange"
import { list } from "../webapi/exchanges"
import Table from "../components/Table"

const ExchangesStyle = styled.div`
  padding: 20px;
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

  useEffect(() => {
    list()
      .then(response => {
        stateFunc(prevState => ({
          ...prevState,
          data: response?.data || []
        }))
      })
  }, [])

  const headers = [
    {
      value: "alias",
      label: "Alias",
      default: true
    },
    {
      value: "provider",
      label: "Provider",
    },
    {
      value: "api_key",
      label: "API Key",
    },
    {
      value: "api_secret",
      label: "API Secret",
    },
    {
      value: "testing_network",
      label: "Testing Network",
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
      row.api_key,
      row.api_secret,
      row.testing_network ? 'Yes' : 'No',
      ''
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
