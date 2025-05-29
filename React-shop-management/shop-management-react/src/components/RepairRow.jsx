import React from 'react';
import MarkAsDoneButton from './MarkAsDoneButton';

function RepairRow({ repair }) {
  return (
    <tr>
      <td>{repair.user_id}</td>
      <td>{repair.service_type}</td>
      <td>{repair.status}</td>
      <td>
        {repair.status !== 'entregue' && (
          <MarkAsDoneButton repairId={repair.request_id} userId={repair.user_id} />
        )}
      </td>
    </tr>
  );
}

export default RepairRow;
