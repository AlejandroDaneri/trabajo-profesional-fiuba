/* Import Libs */
import React, { useState } from "react"
import styled from "styled-components"
import Modal from "../components/reusables/Modal"

/* Import Reusables Components */
import View from "../components/reusables/View"
import Exchange from "./Exchange"

const ExchangesStyle = styled.div`
`

const Exchanges = () => {

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
          </ExchangesStyle>
        }
      />
    </>
  );
};

export default Exchanges;
