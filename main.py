import mido

msg = mido.Message('not_on', note=60)

outputs = mido.get_output_names()
port = mido.open_output(outputs[0])