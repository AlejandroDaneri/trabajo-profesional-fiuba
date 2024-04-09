/* Import Libs */
import ReactAwesomeModal from "react-awesome-modal"
import styled from "styled-components"

const ModalStyle = styled.div`
  background: #282c34;
  border: 1px solid white;

  & .modal-header {
    display: flex;
    align-items: center;
    height: 40px;
    border-bottom: 1px solid white;
    font-size: 18px;
    font-weight: 600;
    padding-left: 10px;
  }

  & .modal-body {
    display: flex;
    justify-content: center;
    background: #282c34;
    width: 100%;
  }
`

const Modal = ({ open, onToggleOpen, title, content, width }) => {
  return (
    <ReactAwesomeModal
      visible={open}
      onClickAway={onToggleOpen}
      width={width || "90%"}
      effect="fadeInUp"
    >
      <ModalStyle>
        <div className="modal-header">{title}</div>
        <div className="modal-body">{content}</div>
      </ModalStyle>
    </ReactAwesomeModal>
  )
}

export default Modal
