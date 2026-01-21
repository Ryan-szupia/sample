import { Alert, Button, SafeAreaView } from 'react-native';
import { login, getProfile } from '@react-native-seoul/kakao-login';

export default function App() {
  const kakaoLogin = async () => {
    try {
      const token = await login();
      Alert.alert('카카오 로그인 성공', JSON.stringify(token, null, 2));

      const profile = await getProfile();
      console.log(profile);
    } catch (e: any) {
      Alert.alert('카카오 로그인 실패', e.message ?? JSON.stringify(e));
    }
  };

  return (
    <SafeAreaView style={{ flex: 1, justifyContent: 'center' }}>
      <Button title="카카오 로그인" onPress={kakaoLogin} />
    </SafeAreaView>
  );
}
