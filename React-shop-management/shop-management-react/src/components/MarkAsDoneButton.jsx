import React from 'react';
import DataPatch from '../utils/DataFetchPut';

function MarkAsDoneButton({ repairId, userId }) {
  const marcar = () => {
    const body = { status: 'entregue' };

    DataPatch(`repairs/${userId}/${repairId}/`, body)
      .then(res => {
        if (res.success === 'yes') {
          alert('Reparação marcada como concluída!');
          window.location.reload();
        }
      });
  };

  return (
    <button onClick={marcar}>Marcar como concluída</button>
  );
}

export default MarkAsDoneButton;
