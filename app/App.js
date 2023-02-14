import * as React from 'react'; import { useState, useEffect, useRef } from 'react'; import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { NavigationContainer } from '@react-navigation/native'; import { Text, View, StyleSheet, TouchableOpacity, Image } from 'react-native'; import Constants from 'expo-constants';
import * as MediaLibrary from 'expo-media-library'; import { MaterialIcons } from '@expo/vector-icons';import Button from './src/components/Camera';
import Cam from './src/components/Camera'; import RecordAud from './src/components/Record'; import Ionicons from '@expo/vector-icons/Ionicons'; 
import { vqaPost } from './req';
//import resp

const Tab = createBottomTabNavigator(); 
export default function App() {
  const [useImage, setuseImage] = useState(null);
  const cam = <Cam setuseImage = {setuseImage}/> 
  const recordaud = <RecordAud useImage = {useImage}/> 
  return (
    <View style={styles.container}>
    <NavigationContainer>
      <Tab.Navigator         
        screenOptions={{
          headerShown: true, 
          tabBarShowLabel: true, 
          tabBarStyle: {backgroundColor: '#000000'}, 
          tabBarInactiveTintColor: '#F05039',
          tabBarActiveTintColor: '#FFFFFF',
          tabBarLabelStyle: {
            fontSize: 26,
          },
          }}>
        <Tab.Screen name="TakePic" children = {()=>cam}/>
        <Tab.Screen name="Prompt" children = {()=> recordaud}/>
      </Tab.Navigator>
    </NavigationContainer>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingTop: Constants.statusBarHeight,
    //paddingBottom: 8,
    backgroundColor: '#000000',
    //padding: 8,
    color: "#ffffff",
  },
  controls: {
    flex: 0.5,
  },
  button: {
    height: 10,
    borderRadius: 6,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontWeight: 'bold',
    fontSize: 30,
    color: '#000000',
    marginLeft: 10,
  },
  camera: {
    flex: 5,
    borderRadius: 20,
  },
  topControls: {
    flex: 1,
  },
});

/* <Popup resp = {resp}/> */
/*export function Popup({resp}) {
  const [isModalVisible, setisModalVisible] = useState(false);

  const toggleModal = () => {
    setisModalVisible(!isModalVisible);
  };

  return (
    <View style={{ flex: 0 }}>
      <Modal isVisible={isModalVisible}>
        <View style={{ flex: 1 }}>
          <Text>{resp}</Text>
          <TouchableOpacity title="Cancel" onPress={toggleModal} style={styles.button}/>
        </View>
      </Modal>
    </View>
  );
}
*/



