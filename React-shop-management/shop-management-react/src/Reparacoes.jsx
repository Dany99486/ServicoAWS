import React, { Component } from "react";
import './App.css';
import DataFetchPut from './utils/DataFetchPut';
import DataFetchPost from './utils/DataFetchPost';
import DataFetchGet from './utils/DataFetchGet';

class Reparacoes extends Component {

  repairs = {
    request_ids: [],
    user_ids: [],
    services: [],
    dates: [],
    slots: [],
    statuses: [],
    costs: [],
    notes: []
  };

  async componentDidMount() {
    try {
      const response = await DataFetchGet('all-repairs/', null);
      //debugger;

      const repairsList = response.data.repairs;
      repairsList.forEach((item) => {
        this.repairs.request_ids.push(item.request_id);
        this.repairs.user_ids.push(item.user_id);
        this.repairs.services.push(item.service_type);
        this.repairs.dates.push(item.appointment_date);
        this.repairs.slots.push(item.time_slot);
        this.repairs.statuses.push(item.status);
        this.repairs.costs.push(item.final_cost);
        this.repairs.notes.push(item.technician_notes);
      });

      this.forceUpdate();
    } catch (error) {
      console.log("Erro ao obter reparações", error);
    }
  }

  async marcarComoConcluida(index) {
    const status = this.repairs.statuses[index];
    const user_id = this.repairs.user_ids[index];
    const request_id = this.repairs.request_ids[index];

    let url = "";
    let body = { user_id, request_id };

    if (status === "aguardando_confirmacao_presenca") {
      url = "client-present/";
      body.presente = true;
    } else if (status === "aguardando_conclusao_reparacao") {
      url = "repair-done/";
    } else if (status === "aguardando_recolha") {
      url = "confirmar-recolha/";
    } else {
      alert("Estado da reparação não suportado.");
      return;
    }

    try {
      const resPost = await DataFetchPost(url, body);
      if (resPost.success === "yes") {
        alert("Reparação atualizada com sucesso!");
        window.location.reload();
      } else {
        alert("Falha ao comunicar com a API.");
      }
    } catch (error) {
      alert("Erro ao comunicar com a API.");
    }
  }
  /*async marcarComoConcluida(index) {
    const bodyPost = {
      user_id: this.repairs.user_ids[index],
      request_id: this.repairs.request_ids[index],
    };

    try {
      const resPost = await DataFetchPost('client-present/', bodyPost);
      if (resPost.success === "yes") {
        alert("Reparação marcada como concluída com sucesso!");
        window.location.reload();
      } else {
        alert("Falha ao confirmar reparação na API.");
      }
    } catch (error) {
      alert("Erro ao comunicar com a API.");
    }
  }*/

  render() {
    const { request_ids, user_ids, services, dates, slots, statuses, costs, notes } = this.repairs;
    const rowCount = request_ids.length;
    
    const serviceNames = {
      screen_replacement: "Substituir Ecrã",
      battery_replacement: "Substituir bateria",
      virus_removal: "Remover Virus",
    };

    const statusNames={
      agendado: "Agendado",
      aguardando_confirmacao_presenca: "Espera Entrega",
      aguardando_pagamento: "Espera Pagamento",
      aguardando_recolha: "Espera Recolha",
      aguardando_aprovacao: "Espera Aprovacao",
      aguardando_conclusao_reparacao: "Espera Conclusão",
      diagnosticado: "Diagnosticado",
      Entregue: "Entregue",
    }

    return (
      <div className="main">
        <div className="mainPage">
          <h1>Gestão de Reparações – PrimeTech</h1>
          <table className="table table-striped">
            <thead>
              <tr>
                {/*<th>Cliente</th>*/}
                <th>Serviço</th>
                <th>Data</th>
                <th>Hora</th>
                <th>Status</th>
                <th>Custo (€)</th>
                <th>Notas</th>
                <th>Ação</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: rowCount }).map((_, i) => (
                <tr key={i}>
                  {/*<td>{user_ids[i]}</td>*/}
                  <td>{serviceNames[services[i]] || services[i]}</td>
                  <td>{dates[i]}</td>
                  <td>{slots[i]}</td>
                  <td>{statusNames[statuses[i]] || statuses[i]}</td>
                  <td>{costs[i] ?? "–"}</td>
                  <td>{notes[i] ?? "–"}</td>
                  <td>
                    {statuses[i] === "aguardando_confirmacao_presenca" && (
                      <button className="finish" onClick={() => this.marcarComoPresente(i)}>
                        Confirmar presença
                      </button>
                    )}
                    {statuses[i] === "aguardando_conclusao_reparacao" && (
                      <button className="finish" onClick={() => this.marcarComoConcluida(i)}>
                        Confirmar Reparação
                      </button>
                    )}
                    {statuses[i] === "aguardando_recolha" && (
                      <button className="finish" onClick={() => this.marcarComoConcluida(i)}>
                        Confirmar Entrega
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

export default Reparacoes;
