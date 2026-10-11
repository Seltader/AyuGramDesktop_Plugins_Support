// This is the source code of AyuGram for Desktop.
//
// We do not and cannot prevent the use of our code,
// but be respectful and credit the original author.
//
// Copyright @Radolyn, 2026
#include "ayu/ui/settings/settings_plugins.h"

#include "ayu/plugins/plugin_manager.h"
#include "ayu/ui/settings/ayu_builder.h"
#include "ayu/ui/settings/settings_ayu_utils.h"
#include "ayu/ui/settings/settings_main.h"
#include "settings/settings_builder.h"
#include "settings/settings_common.h"
#include "styles/style_menu_icons.h"
#include "styles/style_settings.h"
#include "ui/widgets/buttons.h"
#include "ui/widgets/labels.h"
#include "ui/wrap/vertical_layout.h"
#include "window/window_session_controller.h"

#include <QDesktopServices>
#include <QUrl>

namespace Settings {

using namespace Builder;
using namespace AyuBuilder;

namespace {

void BuildInfo(SectionBuilder &builder) {
	builder.add([](const WidgetContext &ctx) -> SectionBuilder::WidgetToAdd {
		return {
			.widget = object_ptr<Ui::FlatLabel>(
				ctx.container,
				rpl::single(QString(
					"Поддержка плагинов на Python (.plugin), "
					"совместимых с exteraGram и мобильным AyuGram.")),
				st::boxLabel),
			.align = style::al_top,
		};
	});

	builder.addSkip();

	const auto dir = AyuPlugins::PluginManager::Instance().pluginsDir();

	builder.addButton({
		.id = u"plugins/open_folder"_q,
		.title = rpl::single(QString("Открыть папку с плагинами")),
		.icon = { &st::menuIconShowInChat },
		.label = rpl::single(QString("plugins/")),
		.onClick = [=] {
			QDesktopServices::openUrl(QUrl::fromLocalFile(dir));
		},
	});

	builder.addButton({
		.id = u"plugins/reload"_q,
		.title = rpl::single(QString("Перезагрузить все плагины")),
		.icon = { &st::menuIconRestore },
		.onClick = [=] {
			AyuPlugins::PluginManager::Instance().reloadPlugins();
		},
	});

	builder.addButton({
		.id = u"plugins/author"_q,
		.title = rpl::single(QString("Разработчик интеграции плагинов")),
		.icon = { &st::menuIconProfile },
		.label = rpl::single(QString("@CallMeSenya")),
		.onClick = [=] {
			QDesktopServices::openUrl(QUrl("https://t.me/CallMeSenya"));
		},
	});
}

void BuildPluginsList(SectionBuilder &builder) {
	builder.addSkip();
	builder.addDivider();
	builder.addSkip();

	builder.addSubsectionTitle(rpl::single(QString("Установленные плагины")));

	const auto plugins = AyuPlugins::PluginManager::Instance().getInstalledPlugins();

	if (plugins.isEmpty()) {
		builder.add([](const WidgetContext &ctx) -> SectionBuilder::WidgetToAdd {
			return {
				.widget = object_ptr<Ui::FlatLabel>(
					ctx.container,
					rpl::single(QString(
						"Плагины не найдены.\n"
						"Поместите файлы .plugin в папку плагинов и нажмите «Перезагрузить» выше.")),
					st::boxLabel),
				.align = style::al_top,
			};
		});
		return;
	}

	for (const auto &plugin : plugins) {
		const auto id = plugin.id;
		auto titleText = plugin.name;
		if (!plugin.version.isEmpty()) {
			titleText += " v" + plugin.version;
		}

		auto subtext = plugin.description;
		if (!plugin.author.isEmpty()) {
			if (!subtext.isEmpty()) subtext += " • ";
			subtext += "Автор: " + plugin.author;
		}

		builder.addButton({
			.id = "plugin/" + id,
			.title = rpl::single(std::move(titleText)),
			.icon = { &st::menuIconBot },
			.label = rpl::single(plugin.enabled ? QString("Активен") : QString("Отключен")),
			.onClick = [=] {
				// Toggle or open plugin settings
			},
		});
	}
}

const auto kMeta = BuildHelper({
	.id = AyuPluginsSection::Id(),
	.parentId = AyuMain::Id(),
	.title = [] { return rpl::single(QString("Плагины")); },
	.icon = &st::menuIconBot,
}, [](SectionBuilder &builder) {
	BuildInfo(builder);
	BuildPluginsList(builder);
});

} // namespace

rpl::producer<QString> AyuPluginsSection::title() {
	return rpl::single(QString("Плагины"));
}

AyuPluginsSection::AyuPluginsSection(
	QWidget *parent,
	not_null<Window::SessionController*> controller)
: Section(parent, controller) {
	setupContent();
}

void AyuPluginsSection::setupContent() {
	const auto content = Ui::CreateChild<Ui::VerticalLayout>(this);
	build(content, kMeta.build);
	Ui::ResizeFitChild(this, content);
}

Type AyuPluginsSectionId() {
	return AyuPluginsSection::Id();
}

} // namespace Settings
