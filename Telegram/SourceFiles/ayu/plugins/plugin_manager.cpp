// This is the source code of AyuGram for Desktop.
//
// We do not and cannot prevent the use of our code,
// but be respectful and credit the original author.
//
// Copyright @Radolyn, 2026
#include "ayu/plugins/plugin_manager.h"

#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QStandardPaths>
#include <QRegularExpression>
#include <QJsonDocument>
#include <QJsonObject>

namespace AyuPlugins {

class PluginManager::Impl {
public:
	Impl() {
		initPaths();
	}

	void initPaths() {
		const auto appData = QStandardPaths::writableLocation(
			QStandardPaths::AppDataLocation);
		_pluginsDir = appData + "/plugins";
		QDir().mkpath(_pluginsDir);
	}

	QString pluginsDir() const {
		return _pluginsDir;
	}

	void scanPlugins() {
		_plugins.clear();
		QDir dir(_pluginsDir);
		const auto entries = dir.entryInfoList(
			QStringList() << "*.plugin" << "*.py",
			QDir::Files);

		for (const auto &info : entries) {
			PluginInfo p;
			p.id = info.baseName();
			p.enabled = true;

			QFile file(info.absoluteFilePath());
			if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
				const auto content = QString::fromUtf8(file.readAll());
				static const auto idRegex = QRegularExpression(R"(__id__\s*=\s*["']([^"']+)["'])");
				static const auto nameRegex = QRegularExpression(R"(__name__\s*=\s*["']([^"']+)["'])");
				static const auto descRegex = QRegularExpression(R"(__description__\s*=\s*["']([^"']+)["'])");
				static const auto authorRegex = QRegularExpression(R"(__author__\s*=\s*["']([^"']+)["'])");
				static const auto versionRegex = QRegularExpression(R"(__version__\s*=\s*["']([^"']+)["'])");

				const auto idMatch = idRegex.match(content);
				if (idMatch.hasMatch()) p.id = idMatch.captured(1);

				const auto nameMatch = nameRegex.match(content);
				p.name = nameMatch.hasMatch() ? nameMatch.captured(1) : p.id;

				const auto descMatch = descRegex.match(content);
				if (descMatch.hasMatch()) p.description = descMatch.captured(1);

				const auto authorMatch = authorRegex.match(content);
				if (authorMatch.hasMatch()) p.author = authorMatch.captured(1);

				const auto verMatch = versionRegex.match(content);
				if (verMatch.hasMatch()) p.version = verMatch.captured(1);
			}
			_plugins.append(p);
		}
	}

	QVector<PluginInfo> plugins() const {
		return _plugins;
	}

	bool onSendMessage(
			int account,
			QString &text,
			EntitiesInText &entities,
			uint64 replyToMsgId) {
		// Hook dispatch to Python plugins
		// When embedded python engine is active, calls on_send_message_hook in plugin_host.py
		return true;
	}

private:
	QString _pluginsDir;
	QVector<PluginInfo> _plugins;
};

PluginManager &PluginManager::Instance() {
	static PluginManager instance;
	return instance;
}

PluginManager::PluginManager() : _impl(std::make_unique<Impl>()) {
}

PluginManager::~PluginManager() = default;

void PluginManager::init() {
	_impl->scanPlugins();
}

void PluginManager::deinit() {
}

bool PluginManager::onSendMessage(
		int account,
		QString &text,
		EntitiesInText &entities,
		uint64 replyToMsgId) {
	return _impl->onSendMessage(account, text, entities, replyToMsgId);
}

QString PluginManager::pluginsDir() const {
	return _impl->pluginsDir();
}

QVector<PluginInfo> PluginManager::getInstalledPlugins() {
	return _impl->plugins();
}

void PluginManager::reloadPlugins() {
	_impl->scanPlugins();
}

void PluginManager::setPluginEnabled(const QString &id, bool enabled) {
	// Toggle plugin state and persist to plugins_settings.json
}

} // namespace AyuPlugins
