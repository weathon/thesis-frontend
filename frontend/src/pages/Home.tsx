import { IonButton, IonCard, IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import ExploreContainer from '../components/ExploreContainer';
import './Home.css';
import { useRef, useState } from 'react';

// https://stackoverflow.com/questions/36280818/how-to-convert-file-to-base64-in-javascript

const Home: React.FC = () => {
  const [base64, setBase64] = useState("")
  function getBase64(file: any) {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
      setBase64(String(reader.result))//.split("base64,")[1])
    };
  }
  const file = useRef(null)
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Image Upload</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Image Upload</IonTitle>
          </IonToolbar>
        </IonHeader>
        <IonCard>
          <div style={{ width: "100%", aspectRatio: 1 / 1, backgroundColor: "lightgray", marginRight: "10%", textAlign: "center" }} onClick={() => {
            //@ts-ignore
            file.current.click()
          }}>
            <img src={base64}></img>
            <div style={{ paddingTop: "40%"}} hidden={base64!=""}><p>Click here to upload</p></div>
            
            <input ref={file} type="file" hidden onChange={()=>
            {
              console.log(1)
            //@ts-ignore
              getBase64(file.current.files[0])
            }}/>
          </div>
        </IonCard>
        <IonButton expand='block' onClick={()=>{
          const submitBase64 = base64.split("base64,")[1]
          // fetch()
        }}>Submit</IonButton>
      </IonContent>
    </IonPage>
  );
};

export default Home;
