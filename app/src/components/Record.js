import { Entypo } from '@expo/vector-icons';
import { MaterialIcons } from '@expo/vector-icons';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { NavigationContainer } from '@react-navigation/native'; 
import { useState, useEffect, useRef } from 'react';
import Constants from 'expo-constants';
import { Camera, CameraType } from 'expo-camera';
import * as MediaLibrary from 'expo-media-library';
import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { ScrollView, Button, TouchableOpacity, StyleSheet, Text, View, Pressable } from 'react-native';
import { Audio } from 'expo-av';
import * as Sharing from 'expo-sharing';
import { color } from 'react-native-reanimated';
import { vqaPost, axois } from '../../req';

export default function RecordAud({useImage}) {
  const [recording, setRecording] = React.useState();
  const [recordings, setRecordings] = React.useState([]);
  const [message, setMessage] = React.useState("");

  async function startRecording() {
    try {
      const permission = await Audio.requestPermissionsAsync();

      if (permission.status === "granted") {
        await Audio.setAudioModeAsync({
          allowsRecordingIOS: true,
          playsInSilentModeIOS: true
        });
        
        const { recording } = await Audio.Recording.createAsync(
          {
          isMeteringEnabled: true,
            android: {
              extension: '.wav',
              outputFormat: Audio.RECORDING_OPTION_ANDROID_OUTPUT_FORMAT_MPEG_4,
              audioEncoder: Audio.RECORDING_OPTION_ANDROID_AUDIO_ENCODER_AMR_NB,
              sampleRate: 44100,
              numberOfChannels: 2,
              bitRate: 128000,
            },
            ios: {
              extension: '.wav',
              audioQuality: Audio.RECORDING_OPTION_IOS_AUDIO_QUALITY_HIGH,
              sampleRate: 44100,
              numberOfChannels: 1,
              bitRate: 128000,
              linearPCMBitDepth: 16,
              linearPCMIsBigEndian: false,
              linearPCMIsFloat: false,
          },
            web: {
              mimeType: 'audio/webm',
              bitsPerSecond: 128000,
            },
          }
        );
        
        setRecording(recording);
        console.log(recording, "12");
      } else {
        setMessage("Please grant permission to app to access microphone");
      }
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  }

  async function stopRecording() {
    setRecording(undefined);
    await recording.stopAndUnloadAsync();

    let updatedRecordings = [...recordings];
    const { sound, status } = await recording.createNewLoadedSoundAsync();
    updatedRecordings.push({
      sound: sound,
      duration: getDurationFormatted(status.durationMillis),
      file: recording.getURI(),

    });

    setRecordings(updatedRecordings);
  }

  function getDurationFormatted(millis) {
    const minutes = millis / 1000 / 60;
    const minutesDisplay = Math.floor(minutes);
    const seconds = Math.round((minutes - minutesDisplay) * 60);
    const secondsDisplay = seconds < 10 ? `0${seconds}` : seconds;
    return `${minutesDisplay}:${secondsDisplay}`;
  }


  function getRecordingLines() {
    return recordings.map((recordingLine, index) => {
      return (
        <View key={index} style={styles.row}>
          <Text style={styles.text}> {index + 1} - {recordingLine.duration}</Text>
          <Pressable style = {styles.button} onPress={() => recordingLine.sound.replayAsync()}><Text style={[{fontWeight: 'bold', fontSize: 34,
    color: '#000000', marginRight: 10, marginLeft: 12,}]}>Play</Text></Pressable>
          <Pressable style = {styles.button} onPress={() => vqaPost(useImage, recordingLine)/*.then(()=> {asdf})*/}><Text style={styles.text}>Ask</Text></Pressable>
        </View>
      );
    });
  } 

  return (
    <ScrollView>
    <View style={styles.text}>
      <Text style={styles.text}>{message}</Text>
      <Button style={styles.button} color={"#000000"}
        
        title={recording ? 'Stop Recording' : 'Start Recording'}
        onPress={recording ? stopRecording : startRecording} 
      />
      {getRecordingLines()}
      <StatusBar style="auto" />
    </View>
    </ScrollView>
  );
  
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  fill: {
    flex: 10,
    margin: 16
  },
  button: {
    margin: 16,
    fontWeight: 'bold',
  },
  text: {
    fontWeight: 'bold',
    fontSize: 34,
    color: '#000000',
    //
    marginRight: 10,
    marginLeft: 12,
  },
  //
});
