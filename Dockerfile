FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    libmagickwand-dev \
    fontconfig \
    wget

ENV OSWALD="https://github.com/google/fonts/raw/master/ofl/oswald/Oswald-Regular.ttf" \
    SOURCE_CODE="https://github.com/google/fonts/raw/master/ofl/sourcecodepro/SourceCodePro-Regular.ttf" \
    DANCING="https://github.com/google/fonts/raw/master/ofl/dancingscript/DancingScript-Regular.ttf" \
    PACIFICO="https://github.com/google/fonts/raw/master/ofl/pacifico/Pacifico-Regular.ttf" \
    COURGETTE="https://github.com/google/fonts/raw/master/ofl/courgette/Courgette-Regular.ttf" \
    ROBOTO="https://github.com/google/fonts/raw/master/apache/robotomono/RobotoMono-Regular.ttf" \
    PTSANS="https://github.com/google/fonts/raw/master/ofl/ptsans/PT_Sans-Web-Regular.ttf" \
    SOFIA="https://github.com/google/fonts/raw/master/ofl/sofia/Sofia-Regular.ttf" \
    FJALLA="https://github.com/google/fonts/raw/master/ofl/fjallaone/FjallaOne-Regular.ttf" \
    LOBSTER="https://github.com/google/fonts/raw/master/ofl/lobster/Lobster-Regular.ttf" \
    MICHROMA="https://github.com/google/fonts/raw/master/ofl/michroma/Michroma.ttf" \
    SQUADA="https://github.com/google/fonts/raw/master/ofl/squadaone/SquadaOne-Regular.ttf" \
    SECULAR="https://github.com/google/fonts/raw/master/ofl/secularone/SecularOne-Regular.ttf" \
    JOSEFIN="https://github.com/google/fonts/raw/master/ofl/josefinslab/JosefinSlab-Regular.ttf" \
    FELL="https://github.com/google/fonts/raw/master/ofl/imfelldwpica/IMFePIrm28P.ttf" \
    COVERED="https://github.com/google/fonts/raw/master/ofl/coveredbyyourgrace/CoveredByYourGrace.ttf"

RUN mkdir -p /usr/share/fonts/ \
    #&& wget -qO- "${SCP_URL}" | tar xz -C /usr/share/fonts \ #  font in zip
    && wget -q "${OSWALD}" -P /usr/share/fonts \
    && wget -q "${PACIFICO}" -P /usr/share/fonts \
    && wget -q "${SOURCE_CODE}" -P /usr/share/fonts \
    && wget -q "${DANCING}" -P /usr/share/fonts \
    && wget -q "${COURGETTE}" -P /usr/share/fonts \
    && wget -q "${ROBOTO}" -P /usr/share/fonts \
    && wget -q "${PTSANS}" -P /usr/share/fonts \
    && wget -q "${SOFIA}" -P /usr/share/fonts \
    && wget -q "${FJALLA}" -P /usr/share/fonts \
    && wget -q "${LOBSTER}" -P /usr/share/fonts \
    && wget -q "${MICHROMA}" -P /usr/share/fonts \
    && wget -q "${SQUADA}" -P /usr/share/fonts \
    && wget -q "${SECULAR}" -P /usr/share/fonts \
    && wget -q "${JOSEFIN}" -P /usr/share/fonts \
    && wget -q "${FELL}" -P /usr/share/fonts \
    && wget -q "${COVERED}" -P /usr/share/fonts

RUN fc-cache -fv

# COPY . .

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py" ]