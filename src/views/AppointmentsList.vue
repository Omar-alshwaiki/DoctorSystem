<template>
  <div>
    <nav class="navbar navbar-light bg-white shadow-sm mb-4">
      <div class="container d-flex justify-content-between align-items-center">
        <span class="fw-bold fs-5">Doctor Appointments</span>
        <router-link to="/" class="btn btn-outline-primary">⇆ Switch Page</router-link>
      </div>
    </nav>

    <div class="container">  
      <div class="card shadow-sm">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">Appointments</h5>
          <button class="btn btn-sm btn-secondary" @click="fetchAppointments">Refresh</button>
        </div>
        <div class="card-body p-0">
          <table class="table table-bordered table-striped mb-0">
            <thead class="table-light">
              <tr>
                <th>Name</th>
                <th>Symptoms</th>
                <th>Time</th>
                <th>Status</th>
                <th>Update</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appointment in appointments" :key="appointment.appointment_id">
                <td>{{ appointment.patientName }}</td>
                <td>{{ appointment.symptoms }}</td>
                <td>{{ appointment.slot }}</td>
                <td>{{ appointment.status }}</td>
                <td>
                  <select class="form-select form-select-sm" :value="appointment.status" @change="e => updateStatus(appointment, e.target.value)">
                    <option value="Pending">Pending</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Completed">Completed</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppointmentsList",
  data() {
    return {
      appointments: []
    };
  },
  mounted() {
    this.fetchAppointments();
  },
  methods: {
    fetchAppointments() {
      fetch("https://e3pn66ir39.execute-api.us-east-1.amazonaws.com/prod/appointments")
        .then(res => res.json())
        .then(data => {
          let list = data.body ? (typeof data.body === 'string' ? JSON.parse(data.body) : data.body) : data;
          if (Array.isArray(list)) {
            this.appointments = list;
          }
        })
        .catch(err => console.error("Error fetching database records:", err));
    },
    updateStatus(appointment, newStatus) {
      // Maps to your correct snake_case primary database key attribute
      const url = `https://e3pn66ir39.execute-api.us-east-1.amazonaws.com/prod/appointments/${appointment.appointment_id}`;
      const payload = { status: newStatus };

      fetch(url, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(async res => {
          const rawBody = await res.text();
          if (!res.ok) throw new Error(`HTTP ${res.status}: ${rawBody}`);
          appointment.status = newStatus;
          alert("Status updated!");
        })
        .catch(err => {
          console.error("Failed to update status:", err);
          alert("Update failed.");
        });
    }
  }
};
</script>
