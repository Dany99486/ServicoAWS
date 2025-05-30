import React, { Component } from "react";
import DataFetchGet from './utils/DataFetchGet';

class Appointments extends Component {

  appointments = {
    dates: [],
    is_available: [],
    request_ids: [],
    time_slots: []
  };

  async componentDidMount() {
    try {
      const response = await DataFetchGet('all-appointments/', null);

      const appointmentsList = response.data.appointments;

      appointmentsList.forEach((item) => {
        this.appointments.dates.push(item.date);
        this.appointments.is_available.push(item.is_available);
        this.appointments.request_ids.push(item.request_id);
        this.appointments.time_slots.push(item.time_slot);
      });

      this.forceUpdate();
    } catch (error) {
      console.log("Erro ao obter agendamentos", error);
    }
  }

  render() {
    const { dates, is_available, request_ids, time_slots } = this.appointments;
    const rowCount = request_ids.length;

    return (
      <div className="main">
        <div className="mainPage">
          <h1>Gestão de Agendamentos – PrimeTech</h1>
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Data</th>
                <th>Horário</th>
                <th>Disponível</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: rowCount }).map((_, i) => (
                <tr key={i}>
                  <td>{dates[i]}</td>
                  <td>{time_slots[i]}</td>
                  <td>{is_available[i] ? "Sim" : "Não"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

export default Appointments;