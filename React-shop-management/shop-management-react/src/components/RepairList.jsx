import React, { useEffect, useState } from 'react';
import DataFetchGet from '../utils/DataFetchGet';
import RepairRow from './RepairRow';

function RepairList({ filter }) {
  const [repairs, setRepairs] = useState([]);

  useEffect(() => {
    DataFetchGet('all-repairs/')
      .then(res => {
        if (res.success === 'yes') {
          const filtered = res.data.filter(r => r.status === filter);
          setRepairs(filtered);
        }
      });
  }, [filter]);

  return (
    <div>
      <h2>{filter.charAt(0).toUpperCase() + filter.slice(1)} Reparações</h2>
      <table>
        <thead>
          <tr>
            <th>Cliente</th>
            <th>Serviço</th>
            <th>Status</th>
            <th>Ação</th>
          </tr>
        </thead>
        <tbody>
          {repairs.map(r => (
            <RepairRow key={r.request_id} repair={r} />
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default RepairList;
