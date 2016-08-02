#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <strings.h>
#include <stdint.h>
#include <stdbool.h>

#include <sys/types.h>
#include <fcntl.h>

#include <pcap.h>

struct usb_pkt {
	uint8_t ignored1[8];
	uint8_t urb_type;
	uint8_t transfer_type;
	uint8_t incoming;
	uint8_t ignored2[21];
	uint32_t urb_length;
	uint32_t data_length;
	uint8_t urb_setup[8];
	uint8_t nothing[16];
	uint8_t data[0];
}__attribute__((__packed__));

static int get_next_pkt(pcap_t *pcap, struct usb_pkt **pkt) {
	int ret;
	struct pcap_pkthdr *header;

	do {
		ret = pcap_next_ex(pcap, &header, (const uint8_t **) pkt);
		if (ret != 1)
			break;

		if (((*pkt)->transfer_type == 3) && ((*pkt)->data_length >= 1)) {
			//printf("found");
			break;

		}

	} while (1);

	return (ret == 1);
}

int main(int argc, char **argv) {
	char *filename;
	char pcap_err[PCAP_ERRBUF_SIZE];
	pcap_t *pcap;
	struct usb_pkt *pkt;
	uint32_t pkt_index = 0;

	if (argc != 2) {
		printf("Usage: %s [dumpfile.pcap]\n", argv[0]);
		return 1;
	}

	filename = argv[1];
	pcap = pcap_open_offline(filename, pcap_err);

	if (!pcap) {
		fprintf(stderr, "Unable to open pcap file: %s\n", pcap_err);
		return 1;
	}
	uint32_t addr;
	uint32_t value32;
	uint16_t value16;

	while (get_next_pkt(pcap, &pkt)) {
		pkt_index++;
		if (pkt->data_length == 1) {
			switch (pkt->data[0]) {

			// mtk_firmware_version = 0xff,
			//case 0xFF:

             //    break:
			//MTK_COMMAND_READ16
			case 0xD0:
				get_next_pkt(pcap, &pkt);  // commmand echo back
				get_next_pkt(pcap, &pkt);  // read address

				memcpy(&addr, pkt->data, 4);

				get_next_pkt(pcap, &pkt);  // read address echo back
				get_next_pkt(pcap, &pkt);  // read length
				get_next_pkt(pcap, &pkt);  // read length echo back
				get_next_pkt(pcap, &pkt);  // dummy
				get_next_pkt(pcap, &pkt);  // read data
				memcpy(&value16, pkt->data, 2);

				get_next_pkt(pcap, &pkt);  // dummy
				printf("val=read16(0x%04x)  # 0x%02x \n", be32toh(addr),
						be16toh(value16));
				break;

				//MTK_COMMAND_WRITE16
			case 0xD2:
				get_next_pkt(pcap, &pkt);  // commmand echo back
				get_next_pkt(pcap, &pkt);  // write address

				memcpy(&addr, pkt->data, 4);

				get_next_pkt(pcap, &pkt);  // write address echo back
				get_next_pkt(pcap, &pkt);  // write length
				get_next_pkt(pcap, &pkt);  // write length echo back
				get_next_pkt(pcap, &pkt);  // dummy
				get_next_pkt(pcap, &pkt);  // write data
				memcpy(&value16, pkt->data, 2);
				get_next_pkt(pcap, &pkt);  // write data echo back
				get_next_pkt(pcap, &pkt);  // dummy
				printf("h.write16(0x%04x,0x%02x) \n", be32toh(addr),
						be16toh(value16));
				break;

				//MTK_COMMAND_WRITE32
			case 0xD4:
				get_next_pkt(pcap, &pkt);  // commmand echo back
				get_next_pkt(pcap, &pkt);  // write address

				memcpy(&addr, pkt->data, 4);

				get_next_pkt(pcap, &pkt);  // write address echo back
				get_next_pkt(pcap, &pkt);  // write length
				get_next_pkt(pcap, &pkt);  // write length echo back
				get_next_pkt(pcap, &pkt);  // dummy
				get_next_pkt(pcap, &pkt);  // write data
				memcpy(&value32, pkt->data, 4);
				get_next_pkt(pcap, &pkt);  // write data echo back
				get_next_pkt(pcap, &pkt);  // dummy
				printf("h.write32(0x%04x,0x%04x)\n", be32toh(addr),
						be32toh(value32));
				break;

				//MTK_COMMAND_READ32 =
			case 0xD1:
				get_next_pkt(pcap, &pkt);  // commmand echo back
				get_next_pkt(pcap, &pkt);  // read address

				memcpy(&addr, pkt->data, 4);

				get_next_pkt(pcap, &pkt);  // read address echo back
				get_next_pkt(pcap, &pkt);  // read length
				get_next_pkt(pcap, &pkt);  // read length echo back
				get_next_pkt(pcap, &pkt);  // dummy
				get_next_pkt(pcap, &pkt);  // read data
				memcpy(&value32, pkt->data, 4);
				get_next_pkt(pcap, &pkt);  // read data echo back
				get_next_pkt(pcap, &pkt);  // dummy
				printf("val=h.read32(0x%04x) # 0x%04x \n", be32toh(addr),
						be32toh(value32));
				break;

				//MTK_COMMAND_WRITE16_OLD
			case 0xA1:

				get_next_pkt(pcap, &pkt);  // commmand echo back
				get_next_pkt(pcap, &pkt);  // write address

				memcpy(&addr, pkt->data, 4);

				get_next_pkt(pcap, &pkt);  // write address echo back
				get_next_pkt(pcap, &pkt);  // write length
				get_next_pkt(pcap, &pkt);  // write length echo back

				get_next_pkt(pcap, &pkt);  // write data
				memcpy(&value16, pkt->data, 2);
				get_next_pkt(pcap, &pkt);  // write data echo back
				printf("h.write16_old(0x%04x,0x%02x)\n", be32toh(addr),
						be16toh(value16));
				break;

				//  MTK_COMMAND_READ16_OLD =
			case 0xA2:
				get_next_pkt(pcap, &pkt);  // commmand echo back
				get_next_pkt(pcap, &pkt);  // read address

				memcpy(&addr, pkt->data, 4);

				get_next_pkt(pcap, &pkt);  // read address echo back
				get_next_pkt(pcap, &pkt);  // read length
				get_next_pkt(pcap, &pkt);  // read length echo back

				get_next_pkt(pcap, &pkt);  // read data
				memcpy(&value16, pkt->data, 2);

				printf("val=h.read16_old(0x%04x) # 0x%02x \n", be32toh(addr),
						be16toh(value16));

				break;

				//  MTK_COMMAND_DOWNLOAD_IMAGE
			case 0xD7:

				get_next_pkt(pcap, &pkt);  // commmand echo back
				get_next_pkt(pcap, &pkt);  // address
				get_next_pkt(pcap, &pkt);  // address echo back

				memcpy(&addr, pkt->data, 4);

				get_next_pkt(pcap, &pkt);  // length
				get_next_pkt(pcap, &pkt);  // length echo back

				memcpy(&value32, pkt->data, 4);

				get_next_pkt(pcap, &pkt);  // signature
				get_next_pkt(pcap, &pkt);  // signature echo back


				printf("# Upload Image to address 0x%04x length 0x%04x \n", be32toh(addr),
										be32toh(value32));




				break;

				// MTK_RUN_CODE
			case 0xd5:
				break;
			default:
				printf("New Commnad %x\n", pkt->data[0]);
				break;

			}
		}


	}

	return 0;
}
