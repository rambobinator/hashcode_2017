inputs = ARGV
index = 0
nb_vid = 0
nb_endpoint = 0
nb_request = 0
nb_cache = 0
cache_size = 0
video_sizes = []
if inputs.length == 1
	if File.file?(inputs[0])
		File.open(inputs[0], "r").each do |data|
			case index
			when 0
				buffer = data.split(' ')
				nb_vid = buffer[0]
				nb_endpoint = buffer[1]
				nb_request = buffer[2]
				nb_cache = buffer[3]
				cache_size = buffer[4]
			when 1
				video_sizes = data.split(' ')
			else
			end
			index += 1	
		end
		p "Videos number: "+nb_vid.to_s
		p "Endpoints number: "+nb_endpoint.to_s
		p "Requests number: "+nb_request.to_s
		p "Cache servers number: "+nb_cache.to_s
		p "Cache server's size: "+cache_size.to_s
		p "Video sizes:"
		p video_sizes
	else
		p "need a file that exists I said"
	end
else
	p "need file name that exists as argument"
end
