import React from 'react';
import './App.css';

class Main extends Component {

  appointments = {
    date: [],
    time_slot: [],
    is_available: [],
    request_id: []
  }

  async componentDidMount() {
    try {
      const response = await DataFetchGet('api/all_appointments', null);

      console.log(response);
      response.data.response.Items.forEach((item, _) => {
        if (!this.appointments.ids.includes(item.id.toString())) {
          this.appointments.ids.push((item.id).toString());
          this.appointments.doctors.push(item.doctor);
          this.appointments.specialitys.push(item.specialty);
          this.appointments.dates.push(item.date);
          this.appointments.hours.push(item.hour);
          this.appointments.rooms.push(item.room);
          this.appointments.states.push(item.status);
        }
      });
      this.forceUpdate()
    } catch (error) {
      console.log("error", error);
    }
  }

  async updateID(id) {
    window.localStorage.setItem("id", id)
  }

  render() {
    const { ids, doctors, specialitys, dates, hours, rooms, states } = this.appointments;
    const appointmentCount = doctors.length;
    return (
      <div className="main">
        <div className="mainPage">
          <h1>Appointments</h1>
          <table className="table table-striped ">
            <thead>
              <tr>
                <th>Id</th>
                <th>Doctor</th>
                <th>Speciality</th>
                <th>Date</th>
                <th>Hour</th>
                <th>Room</th>
                <th>Status</th>
                <th>Finish</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: appointmentCount }).map((_, i) => (
                <tr key={i}>
                  <td>{ids[i]}</td>
                  <td>{doctors[i]}</td>
                  <td>{specialitys[i]}</td>
                  <td>{dates[i]}</td>
                  <td>{hours[i]}</td>
                  <td>{rooms[i]}</td>
                  <td>{states[i]}</td>
                  <td>
                    {states[i] === "schedulled" ? (
                      <button onClick={() => this.updateID(ids[i])} className="finish">Finish</button>
                    ) : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}


const MainPage = () => {

  const [showCamera, setShowCamera] = useState(true);
  const webcamRef = React.useRef(null);

  const capture = React.useCallback(
    () => {
      const imageSrc = webcamRef.current.getScreenshot();
      recon(imageSrc)

      setShowCamera(true);
    },
    [webcamRef]
  )

  async function recon(image) {
    const id = localStorage.getItem("id")
    const data = { "image": image , "id": id}
    try {
      const dataJSON = JSON.stringify(data);
      const a = await DataFetchPut('api/recon', dataJSON)
      if (a.data.status !== 200) {
        window.alert(a.data.response)
        return
      }
      window.alert(a.data.response)
    }
    catch (error) {
      console.log("database unreachable")
    }
  }

  const handleDivClick = (e) => {
    if (e.target.classList.contains('finish')) {
      setShowCamera(false);
    }
  };

  return (
    <>
      <main>
        {showCamera ? (
          <div onClick={handleDivClick}>
            <Main />
          </div>
        ) : (
          <div className="camera">
            <Webcam
              audio={false}
              height={500}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width={720}
              videoConstraints={videoConstraints}
            />
            <button className="finish" onClick={capture}>Capture photo</button>
          </div>
        )}
      </main>
    </>
  )
}

export default MainPage