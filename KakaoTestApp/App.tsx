import React from 'react';
import { View, Button, Alert, StyleSheet } from 'react-native';
import { login } from '@react-native-seoul/kakao-login';

export default function App() {

  const kakaoLogin = async () => {
    try {
      const result = await login();
      console.log('Kakao login success:', result);
      Alert.alert(
      'Kakao Login Success',
      JSON.stringify(result, null, 2)
      );
    } catch (e) {
      console.error('Kakao login error:', e);
      Alert.alert(
      'Kakao Login Failed',
      JSON.stringify(e, null, 2)
      );
    }
  };

  return (
    <View style={styles.container}>
      <Button title="카카오 로그인" onPress={kakaoLogin} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
