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
				printf("Read16  0x%04x 0x%02x \n", be32toh(addr),
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
				printf("Write16 0x%04x 0x%02x \n", be32toh(addr),
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
				printf("Write32 0x%04x 0x%04x \n", be32toh(addr),
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
				printf("Read32  0x%04x 0x%04x \n", be32toh(addr),
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
				printf("Write16 old 0x%04x 0x%02x \n", be32toh(addr),
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

				printf("Read16 old 0x%04x 0x%02x \n", be32toh(addr),
						be16toh(value16));

				break;

				//  MTK_COMMAND_DOWNLOAD_IMAGE
			case 0xD7:
				printf("Upload Image\n\n");

				break;

				// MTK_RUN_CODE
			case 0xd5:
				break;
			default:
				printf("New Commnad %x\n", pkt->data[0]);
				break;

			}
		}

//		if ((pkt->data_length == 1) && (pkt->data[0] == 0xd7)) {
//			uint32_t addr;
//			uint32_t bytes;
//			uint32_t sig_bytes;
//			printf("Found download at offset %d\n", pkt_index);
//
//			get_next_pkt(pcap, &pkt);
//			memcpy(&addr, pkt->data, 4);
//			printf("Writing to address 0x%08x\n", be32toh(addr));
//
//			get_next_pkt(pcap, &pkt);
//			memcpy(&bytes, pkt->data, 4);
//			printf("Writing %d bytes\n", be32toh(bytes));
//
//			get_next_pkt(pcap, &pkt);
//			memcpy(&sig_bytes, pkt->data, 4);
//			printf("Signature is %d bytes\n", be32toh(sig_bytes));
//
//			printf("\n");
//
//			uint8_t data[be32toh(bytes)];
//			uint32_t copied = 0;
//			while (copied < be32toh(bytes)) {
//				int ret;
//				ret = get_next_pkt(pcap, &pkt);
//				if (!ret) {
//					fprintf(stderr, "Packet cut short\n");
//					break;
//				}
//				memcpy(data + copied, pkt->data, pkt->data_length);
//				copied += pkt->data_length;
//			}
//
//			char name[32];
//			snprintf(name, sizeof(name) - 1, "prog-0x%08x", be32toh(addr));
//			int fd = open(name, O_WRONLY | O_CREAT, 0777);
//			if (fd == -1) {
//				perror("Unable to open file for writing");
//				return 1;
//			}
//			write(fd, data, sizeof(data));
//			close(fd);
//		}
	}

	return 0;
}
