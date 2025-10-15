import { datadogRum } from '@datadog/browser-rum';

datadogRum.init({
    applicationId: 'ba828cb5-c3be-45be-8fb6-105fb0ed9ee4',
    clientToken: 'pub9da8e9eff920a0bfe4cf59316c0f92c5',
    site: 'us5.datadoghq.com',
    service: 'pulsefit-gym',
    env: 'production',
    sessionSampleRate: 100,
    sessionReplaySampleRate: 20,
    trackBfcacheViews: true,
    defaultPrivacyLevel: 'mask-user-input',
});

datadogRum.startSessionReplayRecording();
