<template>
        <legend>Signatories</legend>
          <label for="number_of_signatories">Number of signatories</label>
          <input v-model.number="numberOfSignatories"
          type="number" id="number_of_signatories"
          name="number_of_signatories"
          placeholder="Number of signatories" @input="updateSignatories" required />
          <div v-for="(signatory, index) in signatories" :key="index" class="form-group">
            <h3>Signatory {{ index + 1 }}</h3>
            
            <label :for="'name_' + index">Name</label>
            <input
              v-model="signatory.name"
              type="text"
              :id="'name_' + index"
              :name="'name_' + index"
              placeholder="Enter name"
              required
            />

            <label :for="'email_' + index">National ID/Passport</label>
            <input
              v-model="signatory.id_no"
              type="text"
              :id="'id_no_' + index"
              :name="'id_no_' + index"
              placeholder="Enter National ID"
              required
            />

              <label :for="'file_' + index">Upload File</label>
              <input
                type="file"
                :id="'file_' + index"
                :name="'file_' + index"
                @change="handleFileUpload2($event, index)"
                required
              />
            </div>

<button @click="uploadSignatories">
  upload
</button>


</template>

    <script>
    export default {
        name: 'Account_Signatories',
        emits: ['close'],
        data() {
            return {
                numberOfSignatories: 0,
                signatories: []
            }
        },
        methods: {
            handleFileUpload2(event, index) {
      const file = event.target.files[0];
      if (file) {
        this.signatories[index].file = file;
        console.log(file)
      }
    },
      updateSignatories() {
      const updatedNumber = this.numberOfSignatories || 0;
      if (updatedNumber > this.signatories.length) {
        // Add new signatories
        for (let i = this.signatories.length; i < updatedNumber; i++) {
          this.signatories.push({ name: '', id_no: '', file: null });
        }
      } else if (updatedNumber < this.signatories.length) {
        // Remove excess signatories
        this.signatories.splice(updatedNumber);
      }
    },
    async uploadSignatories() {
      this.uploading = true;
      try {
        const formData = new FormData();

        // Append each signatory's details to the FormData
        this.signatories.forEach((signatory) => {
      formData.append("names", signatory.name);
      formData.append("emails", signatory.email);
      formData.append("files", signatory.file);
    });

        // Send the data to the server using Fetch API
        const response = await fetch('http://127.0.0.1:8000/post/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Failed to upload');
        }

        const data = await response.json();
        alert('Upload successful!');
        console.log(data);
      } catch (error) {
        console.error(error);
        alert('Error uploading files. Please try again.');
      } finally {
        this.uploading = false;
      }
    }
        }
    }
</script>
<style scoped>
  input,
  select,
  .head {
    margin: 20px;
  }
  label {
    color: white;
    font-size: 15px;
    margin: 20px;
  }
</style>
