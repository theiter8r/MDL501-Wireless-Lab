% Experiment 2: Basic communication system (Tx -> AWGN channel -> Rx) in MATLAB/Octave
% BPSK modulation, AWGN channel, threshold detection, BER vs Eb/N0.
clc; clear; close all;

N = 2e5;                 % number of bits
EbN0_dB = 0:10;
ber_sim = zeros(size(EbN0_dB));

for k = 1:length(EbN0_dB)
    bits = randi([0 1], 1, N);            % Transmitter: source
    tx = 2*bits - 1;                      % BPSK mapping
    EbN0 = 10^(EbN0_dB(k)/10);
    noise = sqrt(1/(2*EbN0)) * randn(1, N);
    rx = tx + noise;                      % AWGN channel
    bits_hat = rx > 0;                    % Receiver: detector
    ber_sim(k) = sum(bits_hat ~= bits) / N;
end

ber_th = 0.5 * erfc(sqrt(10.^(EbN0_dB/10)));

semilogy(EbN0_dB, ber_th, 'k-', EbN0_dB, ber_sim, 'ro'); grid on;
xlabel('Eb/N0 (dB)'); ylabel('BER');
legend('Theoretical', 'Simulated'); title('BPSK over AWGN');
disp(table(EbN0_dB', ber_sim', ber_th', 'VariableNames', {'EbN0_dB', 'Simulated', 'Theoretical'}));
